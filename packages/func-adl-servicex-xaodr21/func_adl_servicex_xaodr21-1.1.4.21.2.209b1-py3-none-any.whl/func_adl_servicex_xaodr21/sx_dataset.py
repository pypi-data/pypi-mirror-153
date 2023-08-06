from typing import Union
from func_adl_servicex.ServiceX import ServiceXSourceCPPBase
from servicex.servicex import ServiceXDataset
from servicex.utils import DatasetType
from .event_collection import Event


class SXDSAtlasxAODR21(ServiceXSourceCPPBase[Event]):
    def __init__(self, sx: Union[ServiceXDataset, DatasetType], backend="xaod_r21"):
        """
        Create a servicex dataset sequence from a servicex dataset.
        """
        super().__init__(sx, backend, item_type=Event)
