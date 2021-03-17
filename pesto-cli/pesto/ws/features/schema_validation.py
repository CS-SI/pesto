import jsonschema

from pesto.ws.core.pesto_feature import PestoFeature


class SchemaValidation(PestoFeature):
    def __init__(self, schema: dict):
        self.schema = schema

    def process(self, payload: dict) -> dict:
        jsonschema.validate(payload, self.schema)
        return payload
