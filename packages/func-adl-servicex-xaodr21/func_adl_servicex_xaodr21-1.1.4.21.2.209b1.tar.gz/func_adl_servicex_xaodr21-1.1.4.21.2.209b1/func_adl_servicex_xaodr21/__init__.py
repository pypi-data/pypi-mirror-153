from typing import Any, TYPE_CHECKING
from .sx_dataset import SXDSAtlasxAODR21
from .func_adl_iterable import FADLStream
from .trigger import tdt_chain_fired
from .trigger import tmt_match_object
from .type_support import cpp_float, cpp_double, cpp_vfloat, cpp_string, cpp_int
from . import type_support
from .calibration_support import CalibrationEventConfig, calib_tools
atlas_release = "21.2.209"

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
    elementlink_datavector_xaod_btagging_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_btagging_v1__")
    elementlink_datavector_xaod_calocluster_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_calocluster_v1__")
    elementlink_datavector_xaod_eventinfo_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_eventinfo_v1__")
    elementlink_datavector_xaod_iparticle__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_iparticle__")
    elementlink_datavector_xaod_jet_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_jet_v1__")
    elementlink_datavector_xaod_muonsegment_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_muonsegment_v1__")
    elementlink_datavector_xaod_muon_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_muon_v1__")
    elementlink_datavector_xaod_neutralparticle_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_neutralparticle_v1__")
    elementlink_datavector_xaod_pfo_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_pfo_v1__")
    elementlink_datavector_xaod_tautrack_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_tautrack_v1__")
    elementlink_datavector_xaod_trackparticle_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_trackparticle_v1__")
    elementlink_datavector_xaod_truthparticle_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_truthparticle_v1__")
    elementlink_datavector_xaod_truthvertex_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_truthvertex_v1__")
    elementlink_datavector_xaod_vertex_v1__ = _load_me("func_adl_servicex_xaodr21.elementlink_datavector_xaod_vertex_v1__")
    tcomplex = _load_me("func_adl_servicex_xaodr21.tcomplex")
    tlorentzvector = _load_me("func_adl_servicex_xaodr21.tlorentzvector")
    trotation = _load_me("func_adl_servicex_xaodr21.trotation")
    tsqlresult = _load_me("func_adl_servicex_xaodr21.tsqlresult")
    tsqlrow = _load_me("func_adl_servicex_xaodr21.tsqlrow")
    tthread = _load_me("func_adl_servicex_xaodr21.tthread")
    tvector2 = _load_me("func_adl_servicex_xaodr21.tvector2")
    tvector3 = _load_me("func_adl_servicex_xaodr21.tvector3")
    mutex = _load_me("func_adl_servicex_xaodr21.mutex")
    str = _load_me("func_adl_servicex_xaodr21.str")
    vector_elementlink_datavector_xaod_calocluster_v1___ = _load_me("func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_calocluster_v1___")
    vector_elementlink_datavector_xaod_iparticle___ = _load_me("func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_iparticle___")
    vector_elementlink_datavector_xaod_muonsegment_v1___ = _load_me("func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_muonsegment_v1___")
    vector_elementlink_datavector_xaod_neutralparticle_v1___ = _load_me("func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_neutralparticle_v1___")
    vector_elementlink_datavector_xaod_pfo_v1___ = _load_me("func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_pfo_v1___")
    vector_elementlink_datavector_xaod_tautrack_v1___ = _load_me("func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_tautrack_v1___")
    vector_elementlink_datavector_xaod_trackparticle_v1___ = _load_me("func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_trackparticle_v1___")
    vector_elementlink_datavector_xaod_truthparticle_v1___ = _load_me("func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_truthparticle_v1___")
    vector_elementlink_datavector_xaod_truthvertex_v1___ = _load_me("func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_truthvertex_v1___")
    vector_elementlink_datavector_xaod_vertex_v1___ = _load_me("func_adl_servicex_xaodr21.vector_elementlink_datavector_xaod_vertex_v1___")
    vector_root_fit_parametersettings_ = _load_me("func_adl_servicex_xaodr21.vector_root_fit_parametersettings_")
    vector_float_ = _load_me("func_adl_servicex_xaodr21.vector_float_")
    vector_float_ = _load_me("func_adl_servicex_xaodr21.vector_float_")
    vector_int_ = _load_me("func_adl_servicex_xaodr21.vector_int_")
    vector_pair_float_float__ = _load_me("func_adl_servicex_xaodr21.vector_pair_float_float__")
    vector_pair_str_str__ = _load_me("func_adl_servicex_xaodr21.vector_pair_str_str__")
    vector_str_ = _load_me("func_adl_servicex_xaodr21.vector_str_")
    vector_vector_float__ = _load_me("func_adl_servicex_xaodr21.vector_vector_float__")
    vector_xaod_caloclusterbadchanneldata_v1_ = _load_me("func_adl_servicex_xaodr21.vector_xaod_caloclusterbadchanneldata_v1_")
    vector_xaod_eventinfo_v1_streamtag_ = _load_me("func_adl_servicex_xaodr21.vector_xaod_eventinfo_v1_streamtag_")
    vector_xaod_eventinfo_v1_subevent_ = _load_me("func_adl_servicex_xaodr21.vector_xaod_eventinfo_v1_subevent_")
    vector_xaod_jetconstituent_ = _load_me("func_adl_servicex_xaodr21.vector_xaod_jetconstituent_")
else:
    from . import elementlink_datavector_xaod_btagging_v1__
    from . import elementlink_datavector_xaod_calocluster_v1__
    from . import elementlink_datavector_xaod_eventinfo_v1__
    from . import elementlink_datavector_xaod_iparticle__
    from . import elementlink_datavector_xaod_jet_v1__
    from . import elementlink_datavector_xaod_muonsegment_v1__
    from . import elementlink_datavector_xaod_muon_v1__
    from . import elementlink_datavector_xaod_neutralparticle_v1__
    from . import elementlink_datavector_xaod_pfo_v1__
    from . import elementlink_datavector_xaod_tautrack_v1__
    from . import elementlink_datavector_xaod_trackparticle_v1__
    from . import elementlink_datavector_xaod_truthparticle_v1__
    from . import elementlink_datavector_xaod_truthvertex_v1__
    from . import elementlink_datavector_xaod_vertex_v1__
    from . import tcomplex
    from . import tlorentzvector
    from . import trotation
    from . import tsqlresult
    from . import tsqlrow
    from . import tthread
    from . import tvector2
    from . import tvector3
    from . import mutex
    from . import str
    from . import vector_elementlink_datavector_xaod_calocluster_v1___
    from . import vector_elementlink_datavector_xaod_iparticle___
    from . import vector_elementlink_datavector_xaod_muonsegment_v1___
    from . import vector_elementlink_datavector_xaod_neutralparticle_v1___
    from . import vector_elementlink_datavector_xaod_pfo_v1___
    from . import vector_elementlink_datavector_xaod_tautrack_v1___
    from . import vector_elementlink_datavector_xaod_trackparticle_v1___
    from . import vector_elementlink_datavector_xaod_truthparticle_v1___
    from . import vector_elementlink_datavector_xaod_truthvertex_v1___
    from . import vector_elementlink_datavector_xaod_vertex_v1___
    from . import vector_root_fit_parametersettings_
    from . import vector_float_
    from . import vector_float_
    from . import vector_int_
    from . import vector_pair_float_float__
    from . import vector_pair_str_str__
    from . import vector_str_
    from . import vector_vector_float__
    from . import vector_xaod_caloclusterbadchanneldata_v1_
    from . import vector_xaod_eventinfo_v1_streamtag_
    from . import vector_xaod_eventinfo_v1_subevent_
    from . import vector_xaod_jetconstituent_

# Include sub-namespace items
from . import xAOD
from . import std
from . import ROOT