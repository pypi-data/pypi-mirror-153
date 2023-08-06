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
    bindata = _load_me("func_adl_servicex_xaodr21.ROOT.Fit.bindata")
    datarange = _load_me("func_adl_servicex_xaodr21.ROOT.Fit.datarange")
    fitconfig = _load_me("func_adl_servicex_xaodr21.ROOT.Fit.fitconfig")
    fitdata = _load_me("func_adl_servicex_xaodr21.ROOT.Fit.fitdata")
    fitresult = _load_me("func_adl_servicex_xaodr21.ROOT.Fit.fitresult")
    parametersettings = _load_me("func_adl_servicex_xaodr21.ROOT.Fit.parametersettings")
else:
    from . import bindata
    from . import datarange
    from . import fitconfig
    from . import fitdata
    from . import fitresult
    from . import parametersettings

# Include sub-namespace items