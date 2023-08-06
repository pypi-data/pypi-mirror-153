"""
Data from the `$MNI_DATAPATH/surface-extraction` directory.
"""
from civet.extraction.surfaces import RegularSurface
from civet.globals import MNI_DATAPATH


class SurfaceModel(RegularSurface['SurfaceModel']):
    """
    Represents a surface data file from the `$MNI_DATAPATH/surface-extraction` directory.
    """
    @classmethod
    def get_model(cls, name: str) -> 'SurfaceModel':
        return cls(MNI_DATAPATH / 'surface-extraction' / name)


WHITE_MODEL_320 = SurfaceModel.get_model('white_model_320.obj')
