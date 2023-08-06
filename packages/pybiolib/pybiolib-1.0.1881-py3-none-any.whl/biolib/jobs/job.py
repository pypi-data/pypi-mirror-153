from biolib.jobs.job_result import JobResult
from biolib.typing_utils import Optional


class Job:

    def __init__(self, uuid: str):
        self._uuid = uuid

        self._result: Optional[JobResult] = None

    @property
    def result(self) -> JobResult:
        # TODO: Fetch job first and throw error if result not available
        if self._result is None:
            self._result = JobResult(job_uuid=self._uuid)

        return self._result
