from enum import Enum

__NAMESPACE__ = "http://www.sat.gob.mx/sitio_internet/cfd/catalogos"


class CTipoFactor(Enum):
    TASA = "Tasa"
    CUOTA = "Cuota"
    EXENTO = "Exento"
