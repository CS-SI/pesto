import os

from pesto.common.utils import get_logger


class JobListService(object):

    PESTO_WORKSPACE = '/tmp/.pesto/jobs'

    def __init__(self) -> None:
        self.PESTO_WORKSPACE = JobListService.PESTO_WORKSPACE

    def job_list(self, url_root: str) -> dict:
        get_logger().info('job_list : url_root = {}'.format(url_root))

        result = {}

        if os.path.exists(self.PESTO_WORKSPACE):
            get_logger().info('workspace found : {}'.format(self.PESTO_WORKSPACE))
            for job_id in os.listdir(self.PESTO_WORKSPACE):
                result[job_id] = {'link': '{}/api/v1/jobs/{}/status'.format(url_root, job_id)}
        return result
