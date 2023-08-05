from enum import Enum

from biolib.compute_node.webserver.webserver_types import ComputeNodeInfo
from biolib.typing_utils import TypedDict, Optional, List

from biolib.biolib_api_client.app_types import AppVersionOnJob, RemoteHost


class JobState(Enum):
    AWAITING_INPUT = 'awaiting_input'
    CLIENT_ABORTED = 'client_aborted'
    COMPLETED = 'completed'
    FAILED = 'failed'
    IN_PROGRESS = 'in_progress'


class _Job(TypedDict):
    app_version: AppVersionOnJob
    auth_token: str
    caller_job: Optional[str]
    created_at: str
    federated_job_uuid: Optional[str]
    public_id: str
    remote_hosts_with_warning: List[RemoteHost]
    user_id: Optional[str]
    arguments_override_command: bool


# type optional keys with total=False
class Job(_Job, total=False):
    custom_compute_node_url: str


class CloudJob(TypedDict):
    public_id: str
    reserved_cpu_in_nano_shares: int
    reserved_memory_in_bytes: int
    max_runtime_in_seconds: int


class JobWrapper(TypedDict):
    access_token: str
    BASE_URL: str  # TODO: refactor this to lower case
    compute_node_info: Optional[ComputeNodeInfo]
    job: Job
    cloud_job: Optional[CloudJob]
