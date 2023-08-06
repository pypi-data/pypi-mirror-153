from mfire.settings import get_logger
from mfire.text.base import BaseSelector

# Logging
LOGGER = get_logger(name="temperature_selector.mod", bind="temperature_selector")


class TemperatureSelector(BaseSelector):
    """ TemperatureSelector spécifique pour la temperature
    """

    def compute(self, reduction: dict) -> str:
        """ génération du dictionnaire de choix, recherche dans la matrice
        du texte de synthèse pour le température pour détermier la clé du template
        en fonction du paramètre
        """

        LOGGER.info(f"reduction {reduction}")
        key = "P1_Z0"
        mini_low = reduction["general"]["tempe"]["mini"]["low"]
        mini_high = reduction["general"]["tempe"]["mini"]["high"]
        maxi_low = reduction["general"]["tempe"]["maxi"]["low"]
        maxi_high = reduction["general"]["tempe"]["maxi"]["high"]
        if mini_low == mini_high and maxi_low != maxi_high:
            key = "P1_Z0_1MIN"
        elif mini_low != mini_high and maxi_low == maxi_high:
            key = "P1_Z0_1MAX"
        elif mini_low != mini_high and maxi_low == maxi_high:
            key = "P1_Z0_1MIN_1MAX"
        return key
