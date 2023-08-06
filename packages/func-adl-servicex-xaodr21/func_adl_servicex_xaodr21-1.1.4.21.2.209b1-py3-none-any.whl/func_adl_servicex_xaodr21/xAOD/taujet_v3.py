from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'pt': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'pt',
        'return_type': 'double',
    },
    'eta': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'eta',
        'return_type': 'double',
    },
    'phi': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'phi',
        'return_type': 'double',
    },
    'e': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'e',
        'return_type': 'double',
    },
    'm': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'm',
        'return_type': 'double',
    },
    'rapidity': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'rapidity',
        'return_type': 'double',
    },
    'p4': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'p4',
        'return_type': 'const TLorentzVector',
    },
    'ptJetSeed': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'ptJetSeed',
        'return_type': 'double',
    },
    'etaJetSeed': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'etaJetSeed',
        'return_type': 'double',
    },
    'phiJetSeed': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'phiJetSeed',
        'return_type': 'double',
    },
    'mJetSeed': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'mJetSeed',
        'return_type': 'double',
    },
    'ptDetectorAxis': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'ptDetectorAxis',
        'return_type': 'double',
    },
    'etaDetectorAxis': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'etaDetectorAxis',
        'return_type': 'double',
    },
    'phiDetectorAxis': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'phiDetectorAxis',
        'return_type': 'double',
    },
    'mDetectorAxis': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'mDetectorAxis',
        'return_type': 'double',
    },
    'ptIntermediateAxis': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'ptIntermediateAxis',
        'return_type': 'double',
    },
    'etaIntermediateAxis': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'etaIntermediateAxis',
        'return_type': 'double',
    },
    'phiIntermediateAxis': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'phiIntermediateAxis',
        'return_type': 'double',
    },
    'mIntermediateAxis': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'mIntermediateAxis',
        'return_type': 'double',
    },
    'ptTauEnergyScale': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'ptTauEnergyScale',
        'return_type': 'double',
    },
    'etaTauEnergyScale': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'etaTauEnergyScale',
        'return_type': 'double',
    },
    'phiTauEnergyScale': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'phiTauEnergyScale',
        'return_type': 'double',
    },
    'mTauEnergyScale': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'mTauEnergyScale',
        'return_type': 'double',
    },
    'ptTauEtaCalib': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'ptTauEtaCalib',
        'return_type': 'double',
    },
    'etaTauEtaCalib': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'etaTauEtaCalib',
        'return_type': 'double',
    },
    'phiTauEtaCalib': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'phiTauEtaCalib',
        'return_type': 'double',
    },
    'mTauEtaCalib': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'mTauEtaCalib',
        'return_type': 'double',
    },
    'ptPanTauCellBasedProto': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'ptPanTauCellBasedProto',
        'return_type': 'double',
    },
    'etaPanTauCellBasedProto': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'etaPanTauCellBasedProto',
        'return_type': 'double',
    },
    'phiPanTauCellBasedProto': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'phiPanTauCellBasedProto',
        'return_type': 'double',
    },
    'mPanTauCellBasedProto': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'mPanTauCellBasedProto',
        'return_type': 'double',
    },
    'ptPanTauCellBased': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'ptPanTauCellBased',
        'return_type': 'double',
    },
    'etaPanTauCellBased': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'etaPanTauCellBased',
        'return_type': 'double',
    },
    'phiPanTauCellBased': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'phiPanTauCellBased',
        'return_type': 'double',
    },
    'mPanTauCellBased': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'mPanTauCellBased',
        'return_type': 'double',
    },
    'ptTrigCaloOnly': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'ptTrigCaloOnly',
        'return_type': 'double',
    },
    'etaTrigCaloOnly': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'etaTrigCaloOnly',
        'return_type': 'double',
    },
    'phiTrigCaloOnly': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'phiTrigCaloOnly',
        'return_type': 'double',
    },
    'mTrigCaloOnly': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'mTrigCaloOnly',
        'return_type': 'double',
    },
    'ptFinalCalib': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'ptFinalCalib',
        'return_type': 'double',
    },
    'etaFinalCalib': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'etaFinalCalib',
        'return_type': 'double',
    },
    'phiFinalCalib': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'phiFinalCalib',
        'return_type': 'double',
    },
    'mFinalCalib': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'mFinalCalib',
        'return_type': 'double',
    },
    'charge': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'charge',
        'return_type': 'float',
    },
    'ROIWord': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'ROIWord',
        'return_type': 'unsigned int',
    },
    'jetLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'jetLink',
        'return_type': 'const ElementLink<DataVector<xAOD::Jet_v1>>',
    },
    'jet': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'jet',
        'return_type': 'const xAOD::Jet_v1*',
    },
    'vertexLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'vertexLink',
        'return_type': 'const ElementLink<DataVector<xAOD::Vertex_v1>>',
    },
    'vertex': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'vertex',
        'return_type': 'const xAOD::Vertex_v1*',
    },
    'secondaryVertexLink': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'secondaryVertexLink',
        'return_type': 'const ElementLink<DataVector<xAOD::Vertex_v1>>',
    },
    'secondaryVertex': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'secondaryVertex',
        'return_type': 'const xAOD::Vertex_v1*',
    },
    'tauTrackLinksWithMask': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'tauTrackLinksWithMask',
        'return_type_element': 'ElementLink<DataVector<xAOD::TauTrack_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::TauTrack_v1>>>',
    },
    'allTauTrackLinksNonConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'allTauTrackLinksNonConst',
        'return_type_element': 'ElementLink<DataVector<xAOD::TauTrack_v1>>',
        'return_type_collection': 'vector<ElementLink<DataVector<xAOD::TauTrack_v1>>>',
    },
    'allTauTrackLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'allTauTrackLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::TauTrack_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::TauTrack_v1>>>',
    },
    'trackWithMask': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'trackWithMask',
        'return_type': 'const xAOD::TauTrack_v1*',
    },
    'nTracksCharged': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nTracksCharged',
        'return_type': 'int',
    },
    'nTracksIsolation': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nTracksIsolation',
        'return_type': 'int',
    },
    'nTracksWithMask': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nTracksWithMask',
        'return_type': 'int',
    },
    'nAllTracks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nAllTracks',
        'return_type': 'int',
    },
    'clusterLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'clusterLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::IParticle>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::IParticle>>>',
    },
    'cluster': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'cluster',
        'return_type': 'const xAOD::IParticle*',
    },
    'nClusters': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nClusters',
        'return_type': 'int',
    },
    'pi0Links': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'pi0Links',
        'return_type_element': 'ElementLink<DataVector<xAOD::IParticle>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::IParticle>>>',
    },
    'pi0': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'pi0',
        'return_type': 'const xAOD::IParticle*',
    },
    'nPi0s': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nPi0s',
        'return_type': 'int',
    },
    'trackFilterProngs': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'trackFilterProngs',
        'return_type': 'int',
    },
    'trackFilterQuality': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'trackFilterQuality',
        'return_type': 'int',
    },
    'pi0ConeDR': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'pi0ConeDR',
        'return_type': 'float',
    },
    'hadronicPFOLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'hadronicPFOLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::PFO_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::PFO_v1>>>',
    },
    'hadronicPFO': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'hadronicPFO',
        'return_type': 'const xAOD::PFO_v1*',
    },
    'nHadronicPFOs': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nHadronicPFOs',
        'return_type': 'int',
    },
    'shotPFOLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'shotPFOLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::PFO_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::PFO_v1>>>',
    },
    'shotPFO': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'shotPFO',
        'return_type': 'const xAOD::PFO_v1*',
    },
    'nShotPFOs': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nShotPFOs',
        'return_type': 'int',
    },
    'chargedPFOLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'chargedPFOLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::PFO_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::PFO_v1>>>',
    },
    'chargedPFO': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'chargedPFO',
        'return_type': 'const xAOD::PFO_v1*',
    },
    'nChargedPFOs': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nChargedPFOs',
        'return_type': 'int',
    },
    'neutralPFOLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'neutralPFOLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::PFO_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::PFO_v1>>>',
    },
    'neutralPFO': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'neutralPFO',
        'return_type': 'const xAOD::PFO_v1*',
    },
    'nNeutralPFOs': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nNeutralPFOs',
        'return_type': 'int',
    },
    'pi0PFOLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'pi0PFOLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::PFO_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::PFO_v1>>>',
    },
    'pi0PFO': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'pi0PFO',
        'return_type': 'const xAOD::PFO_v1*',
    },
    'nPi0PFOs': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nPi0PFOs',
        'return_type': 'int',
    },
    'protoChargedPFOLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'protoChargedPFOLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::PFO_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::PFO_v1>>>',
    },
    'protoChargedPFO': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'protoChargedPFO',
        'return_type': 'const xAOD::PFO_v1*',
    },
    'nProtoChargedPFOs': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nProtoChargedPFOs',
        'return_type': 'int',
    },
    'protoNeutralPFOLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'protoNeutralPFOLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::PFO_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::PFO_v1>>>',
    },
    'protoNeutralPFO': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'protoNeutralPFO',
        'return_type': 'const xAOD::PFO_v1*',
    },
    'nProtoNeutralPFOs': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nProtoNeutralPFOs',
        'return_type': 'int',
    },
    'protoPi0PFOLinks': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'protoPi0PFOLinks',
        'return_type_element': 'ElementLink<DataVector<xAOD::PFO_v1>>',
        'return_type_collection': 'const vector<ElementLink<DataVector<xAOD::PFO_v1>>>',
    },
    'protoPi0PFO': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'protoPi0PFO',
        'return_type': 'const xAOD::PFO_v1*',
    },
    'nProtoPi0PFOs': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'nProtoPi0PFOs',
        'return_type': 'int',
    },
    'index': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'index',
        'return_type': 'int',
    },
    'usingPrivateStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'usingPrivateStore',
        'return_type': 'bool',
    },
    'usingStandaloneStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'usingStandaloneStore',
        'return_type': 'bool',
    },
    'hasStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'hasStore',
        'return_type': 'bool',
    },
    'hasNonConstStore': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'hasNonConstStore',
        'return_type': 'bool',
    },
    'clearDecorations': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'clearDecorations',
        'return_type': 'bool',
    },
    'auxdataConst': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'auxdataConst',
        'return_type': 'U',
    },
    'isAvailable': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'xAOD::TauJet_v3',
        'method_name': 'isAvailable',
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
        s_update = s_update.MetaData({
            'metadata_type': 'inject_code',
            'name': 'xAODTau/versions/TauJet_v3.h',
            'body_includes': ["xAODTau/versions/TauJet_v3.h"],
        })
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class TauJet_v3:
    "A class"

    def pt(self) -> float:
        "A method"
        ...

    def eta(self) -> float:
        "A method"
        ...

    def phi(self) -> float:
        "A method"
        ...

    def e(self) -> float:
        "A method"
        ...

    def m(self) -> float:
        "A method"
        ...

    def rapidity(self) -> float:
        "A method"
        ...

    def p4(self) -> func_adl_servicex_xaodr21.tlorentzvector.TLorentzVector:
        "A method"
        ...

    def ptJetSeed(self) -> float:
        "A method"
        ...

    def etaJetSeed(self) -> float:
        "A method"
        ...

    def phiJetSeed(self) -> float:
        "A method"
        ...

    def mJetSeed(self) -> float:
        "A method"
        ...

    def ptDetectorAxis(self) -> float:
        "A method"
        ...

    def etaDetectorAxis(self) -> float:
        "A method"
        ...

    def phiDetectorAxis(self) -> float:
        "A method"
        ...

    def mDetectorAxis(self) -> float:
        "A method"
        ...

    def ptIntermediateAxis(self) -> float:
        "A method"
        ...

    def etaIntermediateAxis(self) -> float:
        "A method"
        ...

    def phiIntermediateAxis(self) -> float:
        "A method"
        ...

    def mIntermediateAxis(self) -> float:
        "A method"
        ...

    def ptTauEnergyScale(self) -> float:
        "A method"
        ...

    def etaTauEnergyScale(self) -> float:
        "A method"
        ...

    def phiTauEnergyScale(self) -> float:
        "A method"
        ...

    def mTauEnergyScale(self) -> float:
        "A method"
        ...

    def ptTauEtaCalib(self) -> float:
        "A method"
        ...

    def etaTauEtaCalib(self) -> float:
        "A method"
        ...

    def phiTauEtaCalib(self) -> float:
        "A method"
        ...

    def mTauEtaCalib(self) -> float:
        "A method"
        ...

    def ptPanTauCellBasedProto(self) -> float:
        "A method"
        ...

    def etaPanTauCellBasedProto(self) -> float:
        "A method"
        ...

    def phiPanTauCellBasedProto(self) -> float:
        "A method"
        ...

    def mPanTauCellBasedProto(self) -> float:
        "A method"
        ...

    def ptPanTauCellBased(self) -> float:
        "A method"
        ...

    def etaPanTauCellBased(self) -> float:
        "A method"
        ...

    def phiPanTauCellBased(self) -> float:
        "A method"
        ...

    def mPanTauCellBased(self) -> float:
        "A method"
        ...

    def ptTrigCaloOnly(self) -> float:
        "A method"
        ...

    def etaTrigCaloOnly(self) -> float:
        "A method"
        ...

    def phiTrigCaloOnly(self) -> float:
        "A method"
        ...

    def mTrigCaloOnly(self) -> float:
        "A method"
        ...

    def ptFinalCalib(self) -> float:
        "A method"
        ...

    def etaFinalCalib(self) -> float:
        "A method"
        ...

    def phiFinalCalib(self) -> float:
        "A method"
        ...

    def mFinalCalib(self) -> float:
        "A method"
        ...

    def charge(self) -> float:
        "A method"
        ...

    def ROIWord(self) -> int:
        "A method"
        ...

    def jetLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_jet_v1__.ElementLink_DataVector_xAOD_Jet_v1__:
        "A method"
        ...

    def jet(self) -> func_adl_servicex_xaodr21.xAOD.jet_v1.Jet_v1:
        "A method"
        ...

    def vertexLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_vertex_v1__.ElementLink_DataVector_xAOD_Vertex_v1__:
        "A method"
        ...

    def vertex(self) -> func_adl_servicex_xaodr21.xAOD.vertex_v1.Vertex_v1:
        "A method"
        ...

    def secondaryVertexLink(self) -> func_adl_servicex_xaodr21.elementlink_datavector_xaod_vertex_v1__.ElementLink_DataVector_xAOD_Vertex_v1__:
        "A method"
        ...

    def secondaryVertex(self) -> func_adl_servicex_xaodr21.xAOD.vertex_v1.Vertex_v1:
        "A method"
        ...

    def tauTrackLinksWithMask(self, noname_arg: int) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_tautrack_v1___.vector_ElementLink_DataVector_xAOD_TauTrack_v1___:
        "A method"
        ...

    def allTauTrackLinksNonConst(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_tautrack_v1___.vector_ElementLink_DataVector_xAOD_TauTrack_v1___:
        "A method"
        ...

    def allTauTrackLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_tautrack_v1___.vector_ElementLink_DataVector_xAOD_TauTrack_v1___:
        "A method"
        ...

    def trackWithMask(self, i: int, mask: int, container_index: int) -> func_adl_servicex_xaodr21.xAOD.tautrack_v1.TauTrack_v1:
        "A method"
        ...

    def nTracksCharged(self) -> int:
        "A method"
        ...

    def nTracksIsolation(self) -> int:
        "A method"
        ...

    def nTracksWithMask(self, classification: int) -> int:
        "A method"
        ...

    def nAllTracks(self) -> int:
        "A method"
        ...

    def clusterLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_iparticle___.vector_ElementLink_DataVector_xAOD_IParticle___:
        "A method"
        ...

    def cluster(self, i: int) -> func_adl_servicex_xaodr21.xAOD.iparticle.IParticle:
        "A method"
        ...

    def nClusters(self) -> int:
        "A method"
        ...

    def pi0Links(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_iparticle___.vector_ElementLink_DataVector_xAOD_IParticle___:
        "A method"
        ...

    def pi0(self, i: int) -> func_adl_servicex_xaodr21.xAOD.iparticle.IParticle:
        "A method"
        ...

    def nPi0s(self) -> int:
        "A method"
        ...

    def trackFilterProngs(self) -> int:
        "A method"
        ...

    def trackFilterQuality(self) -> int:
        "A method"
        ...

    def pi0ConeDR(self) -> float:
        "A method"
        ...

    def hadronicPFOLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_pfo_v1___.vector_ElementLink_DataVector_xAOD_PFO_v1___:
        "A method"
        ...

    def hadronicPFO(self, i: int) -> func_adl_servicex_xaodr21.xAOD.pfo_v1.PFO_v1:
        "A method"
        ...

    def nHadronicPFOs(self) -> int:
        "A method"
        ...

    def shotPFOLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_pfo_v1___.vector_ElementLink_DataVector_xAOD_PFO_v1___:
        "A method"
        ...

    def shotPFO(self, i: int) -> func_adl_servicex_xaodr21.xAOD.pfo_v1.PFO_v1:
        "A method"
        ...

    def nShotPFOs(self) -> int:
        "A method"
        ...

    def chargedPFOLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_pfo_v1___.vector_ElementLink_DataVector_xAOD_PFO_v1___:
        "A method"
        ...

    def chargedPFO(self, i: int) -> func_adl_servicex_xaodr21.xAOD.pfo_v1.PFO_v1:
        "A method"
        ...

    def nChargedPFOs(self) -> int:
        "A method"
        ...

    def neutralPFOLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_pfo_v1___.vector_ElementLink_DataVector_xAOD_PFO_v1___:
        "A method"
        ...

    def neutralPFO(self, i: int) -> func_adl_servicex_xaodr21.xAOD.pfo_v1.PFO_v1:
        "A method"
        ...

    def nNeutralPFOs(self) -> int:
        "A method"
        ...

    def pi0PFOLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_pfo_v1___.vector_ElementLink_DataVector_xAOD_PFO_v1___:
        "A method"
        ...

    def pi0PFO(self, i: int) -> func_adl_servicex_xaodr21.xAOD.pfo_v1.PFO_v1:
        "A method"
        ...

    def nPi0PFOs(self) -> int:
        "A method"
        ...

    def protoChargedPFOLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_pfo_v1___.vector_ElementLink_DataVector_xAOD_PFO_v1___:
        "A method"
        ...

    def protoChargedPFO(self, i: int) -> func_adl_servicex_xaodr21.xAOD.pfo_v1.PFO_v1:
        "A method"
        ...

    def nProtoChargedPFOs(self) -> int:
        "A method"
        ...

    def protoNeutralPFOLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_pfo_v1___.vector_ElementLink_DataVector_xAOD_PFO_v1___:
        "A method"
        ...

    def protoNeutralPFO(self, i: int) -> func_adl_servicex_xaodr21.xAOD.pfo_v1.PFO_v1:
        "A method"
        ...

    def nProtoNeutralPFOs(self) -> int:
        "A method"
        ...

    def protoPi0PFOLinks(self) -> func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_pfo_v1___.vector_ElementLink_DataVector_xAOD_PFO_v1___:
        "A method"
        ...

    def protoPi0PFO(self, i: int) -> func_adl_servicex_xaodr21.xAOD.pfo_v1.PFO_v1:
        "A method"
        ...

    def nProtoPi0PFOs(self) -> int:
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
