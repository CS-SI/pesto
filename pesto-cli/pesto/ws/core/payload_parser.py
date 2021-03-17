
from enum import Enum
from typing import Dict

from pesto.common.utils import get_logger
from pesto.ws.core.pesto_feature import PestoFeature
from pesto.ws.features.converter.image.image_roi import ImageROI


class PestoConfig(Enum):
    __order__ = ['roi']
    roi = ImageROI

    def build(self, param):
        return self.value(param)


class PayloadParser(object):
    PIPELINE = ['roi']
    FEATURES = {
        'roi': ImageROI
    }

    @staticmethod
    def parse(payload: dict) -> Dict[PestoConfig, PestoFeature]:
        get_logger().info('pesto features extraction ...')

        config = payload.pop('pesto') if 'pesto' in payload else {}

        features = {
            item: item.build(config[item.name])
            for item in PestoConfig if item.name in config
        }
        for name in filter(lambda _: _ in config, PayloadParser.PIPELINE):
            features[name] = PayloadParser.FEATURES[name](config[name])
        return features
