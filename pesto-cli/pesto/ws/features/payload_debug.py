from pesto.ws.core.pesto_feature import PestoFeature
from pesto.common.utils import get_logger


class PayloadDebug(PestoFeature):
    def __init__(self, schema: dict):
        self.schema = schema

    def process(self, payload: dict) -> dict:
        get_logger().info('listing inputs')
        for key, value in self.schema['properties'].items():
            key_type = value.get('$ref', value)
            try:
                key_infos = payload[key].shape
            except:
                key_infos = 'json'
            get_logger().info('{} : {} : {}'.format(key, key_type, key_infos))
        return payload
