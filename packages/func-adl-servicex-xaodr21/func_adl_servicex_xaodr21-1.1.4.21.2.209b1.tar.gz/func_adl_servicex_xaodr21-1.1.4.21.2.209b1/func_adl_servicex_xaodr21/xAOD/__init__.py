from typing import Any, TYPE_CHECKING

class _load_me:
    """Python's type resolution system demands that types be already loaded
    when they are resolved by the type hinting system. Unfortunately,
    for us to do that for classes with circular references, this fails. In order
    to have everything loaded, we would be triggering the circular references
    during the import process.

    This loader gets around that by delay-loading the files that contain the
    classes, but also tapping into anyone that wants to load the classes.
    """

    def __init__(self, name: str):
        self._name = name
        self._loaded = None

    def __getattr__(self, __name: str) -> Any:
        if self._loaded is None:
            import importlib

            self._loaded = importlib.import_module(self._name)
        return getattr(self._loaded, __name)


# Class loads. We do this to both enable type checking and also
# get around potential circular references in the C++ data model.
if not TYPE_CHECKING:
    btagvertex_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.btagvertex_v1")
    btagging_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.btagging_v1")
    caloclusterbadchanneldata_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.caloclusterbadchanneldata_v1")
    calocluster_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.calocluster_v1")
    calotower_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.calotower_v1")
    ditaujet_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.ditaujet_v1")
    egamma_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.egamma_v1")
    electron_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.electron_v1")
    eventinfo_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.eventinfo_v1")
    iparticle = _load_me("func_adl_servicex_xaodr21.xAOD.iparticle")
    jetconstituent = _load_me("func_adl_servicex_xaodr21.xAOD.jetconstituent")
    jetconstituentvector = _load_me("func_adl_servicex_xaodr21.xAOD.jetconstituentvector")
    jet_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.jet_v1")
    missinget_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.missinget_v1")
    muonsegment_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.muonsegment_v1")
    muon_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.muon_v1")
    neutralparticle_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.neutralparticle_v1")
    pfo_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.pfo_v1")
    photon_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.photon_v1")
    slowmuon_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.slowmuon_v1")
    taujet_v3 = _load_me("func_adl_servicex_xaodr21.xAOD.taujet_v3")
    tautrack_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.tautrack_v1")
    trackcalocluster_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.trackcalocluster_v1")
    trackparticle_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.trackparticle_v1")
    trutheventbase_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.trutheventbase_v1")
    truthevent_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.truthevent_v1")
    truthmetadata_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.truthmetadata_v1")
    truthparticle_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.truthparticle_v1")
    truthvertex_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.truthvertex_v1")
    vertex_v1 = _load_me("func_adl_servicex_xaodr21.xAOD.vertex_v1")
else:
    from . import btagvertex_v1
    from . import btagging_v1
    from . import caloclusterbadchanneldata_v1
    from . import calocluster_v1
    from . import calotower_v1
    from . import ditaujet_v1
    from . import egamma_v1
    from . import electron_v1
    from . import eventinfo_v1
    from . import iparticle
    from . import jetconstituent
    from . import jetconstituentvector
    from . import jet_v1
    from . import missinget_v1
    from . import muonsegment_v1
    from . import muon_v1
    from . import neutralparticle_v1
    from . import pfo_v1
    from . import photon_v1
    from . import slowmuon_v1
    from . import taujet_v3
    from . import tautrack_v1
    from . import trackcalocluster_v1
    from . import trackparticle_v1
    from . import trutheventbase_v1
    from . import truthevent_v1
    from . import truthmetadata_v1
    from . import truthparticle_v1
    from . import truthvertex_v1
    from . import vertex_v1

# Include sub-namespace items
from . import EventInfo_v1
from . import TruthEvent_v1
from . import TruthParticle_v1