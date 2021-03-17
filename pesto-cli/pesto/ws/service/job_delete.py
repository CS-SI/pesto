import os
import shutil

from pesto.common.utils import get_logger
from pesto.ws.service.job_list import JobListService


class JobDeleteService:
    def __init__(self, url_root: str, job_id: str):
        self.job_id = job_id
        self.job_path = os.path.join(JobListService.PESTO_WORKSPACE, self.job_id)
        self.url_root = url_root

    def delete(self) -> None:
        get_logger().info('delete: job_id = {}'.format(self.job_id))
        shutil.rmtree(self.job_path)

    def delete_partial(self, result_id: str) -> None:
        for ext in [
            'json',
            'tif', 'jpeg', 'png',
            'float', 'int', 'string'
        ]:
            _remove_silent(os.path.join(self.job_path, result_id + '.' + ext))


def _remove_silent(path: str) -> None:
    try:
        os.remove(path)
    except:
        pass
