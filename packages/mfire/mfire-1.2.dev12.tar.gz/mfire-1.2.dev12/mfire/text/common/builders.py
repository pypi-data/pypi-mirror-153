from mfire.settings import get_logger
from mfire.text.base import BaseBuilder
from mfire.text.period_describer import PeriodDescriber
from mfire.utils.date import Period


# Logging
LOGGER = get_logger(name="common_builder.mod", bind="common_builder")


class SynonymeBuilder(BaseBuilder):
    """ SynonymeBuilder qui doit construire les synonyme du texte de synthèse
    """

    def find_synonyme(self):
        pass

    def compute(self):

        self.find_synonyme()


class PeriodBuilder(BaseBuilder):
    """ PeriodBuilder qui doit construire les périodes du texte de synthèse
    """

    def build_period(self, reduction):
        prod_date = reduction["meta"]["production_datetime"]
        period = PeriodDescriber(prod_date).describe(
            Period(reduction["general"]["start"], reduction["general"]["stop"])
        )

        self._text = self._text.format(period=period)

    def compute(self):

        self.build_period()


class ZoneBuilder(BaseBuilder):
    """ ZoneBuilder qui doit construire les zones du texte de synthèse
    """

    def build_zone(self):
        pass

    def compute(self):

        self.build_zone()
