from typing import Any

from pesto.common.utils import get_logger
from pesto.ws.core.pesto_feature import PestoFeature
from pesto.ws.service.job_result import ResultType


class StatefulResponse(PestoFeature):

    def __init__(self, url_root: str, job_id: str):
        self.url_root = url_root
        self.job_id = job_id

    def process(self, payload: dict) -> Any:
        get_logger().info('response mode : stateful')
        return {
                   'link': '{}/api/v1/jobs/{}/status'.format(self.url_root, self.job_id)
               }, ResultType.json
